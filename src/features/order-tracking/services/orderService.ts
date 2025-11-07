export async function getOrder(orderId: number) {
  return { orderId, status: 'created' };
}
